from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import multiprocessing
import os
from core.notification.notification_system import NotificationSystem
from utils.constants import MIN_VIDEO_SECONDS
from proglog import ProgressBarLogger

notification_system = NotificationSystem()
progress_bar_indicator = 't'

class CustomizedProgressBarLogger(ProgressBarLogger):
   
    def bars_callback(self, bar, attr, value, old_value=None):
        percentage = (value / self.bars[bar]['total']) * 100

        progress_min = 60
        progress_max = 100
        adjusted_percentage = progress_min + (percentage / 100) * (progress_max - progress_min)
    
        if bar == progress_bar_indicator: 
            notification_system.notify_progress_bar(f"Gerando vídeo final", int(adjusted_percentage))

logger = CustomizedProgressBarLogger()

def cut_video(video, cuts):
    cut_segments = []
    for cut in cuts:
        start_time = cut.get("start")
        end_time = cut.get("end")
        if start_time < 0: 
            start_time = 0
        if end_time > video.duration:
            end_time = video.duration
            
        segment = video.subclip(start_time, end_time)
        cut_segments.append(segment)
    return (cut_segments, sum(i['cuts_count'] for i in cuts))

def generate_video(combined_videos, times_of_each_cut, dir_to_save, config):
    cut_segments = []
    cut_segments, total_cuts = cut_video(combined_videos, times_of_each_cut)
    if not cut_segments:
        notification_system.notify("Nenhum corte encontrado")
    else:
        notification_system.notify(f"{total_cuts} cortes foram encontrados no vídeo {config['final_video_name']}")
        concatenated_videoclips = concatenate_videoclips(cut_segments) 
        if config['flip'] is True:
            concatenated_videoclips = concatenated_videoclips.add_mask().rotate(180)
        logger = CustomizedProgressBarLogger()
        num_threads = max(1, multiprocessing.cpu_count() - 1)
        concatenated_videoclips.write_videofile(f"{dir_to_save}{os.sep}{config['final_video_name']}.mp4", threads=num_threads, preset='ultrafast', logger=logger)
    return (total_cuts, sum(i['end'] - i['start'] for i in times_of_each_cut))

def merge_videos(videos_paths):
    videos = []
    invalid_videos = []  

    for video_path in videos_paths:
        try:
            video = VideoFileClip(video_path)
            if video.duration >= MIN_VIDEO_SECONDS:
                videos.append(video)
            else:
                notification_system.notify(f"Ignorando o vídeo {video_path} com {video.duration} segundos por ter menos de {MIN_VIDEO_SECONDS} segundos, menor que o mínimo permitido")
                invalid_videos.append(video_path)
        except Exception as e:
            notification_system.notify(f"Erro no carregamento do vídeo: {video_path} por ter algum erro no formato do vídeo.")
            invalid_videos.append(video_path) 
    
    videos_paths[:] = [video for video in videos_paths if video not in invalid_videos]
    
    ## TODO: DAR UM JEITO DE FECHAR OS VÍDEOS, TEM ALGUNS CASOS QUE DÁ ERRO NO FINAL DO PROCESSO
    # for video in videos:
    #     video.close()  
    
    if len(videos) == 1:
        return videos[0] 
    
    notification_system.notify(f"Iniciando mesclagem de '{len(videos)}' vídeos")
    return concatenate_videoclips(videos)
