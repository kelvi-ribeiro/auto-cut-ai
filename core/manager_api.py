
from core.notification.notification_system import NotificationSystem
import core.video_manipulation_api as video_manipulation
from core.gesture_recognition.gesture_recognition import GestureRecognition
from core.blink_screen_recognition import BlinkScreenRecognition
from core.voice_recognition import VoiceRecognition
import utils.generic_utils as generic_utils
import datetime as dt
import os
from utils.constants import EXPORT_PATH
from utils.datetime_utils import get_datetime_without_milliseconds
from utils.number_utils  import get_pretty_minutes
from utils.email_utils import send_email
from utils.file_utils import get_result_file, save_result_file

notification_system = NotificationSystem()

def generate_cut_video(config, files, dir_to_save, combined_videos): 
    recognition_type = config["recognition_type"]
    use_saved_result_file = config["use_saved_result_file"]
    final_video_name = config["final_video_name"]
    about_to_process_message = f"Iniciando processamento do vídeo {final_video_name}. "
    notification_system.notify(about_to_process_message)
    send_email(config, f"{final_video_name} atualização no status de processamento", about_to_process_message)
    times_of_each_cut = []
    if not use_saved_result_file:
        if recognition_type == "voice_recognition":
            recognition_processor = VoiceRecognition(files, config, notification_system, combined_videos)
        elif recognition_type == "gesture_recognition":
            recognition_processor = GestureRecognition(files, config, notification_system)
        else: 
            recognition_processor = BlinkScreenRecognition(files, config, notification_system)
            
        times_of_each_cut = recognition_processor.process()
        save_result_file(times_of_each_cut, final_video_name)
    else:
        times_of_each_cut = get_result_file(final_video_name)
    return video_manipulation.generate_video(combined_videos, times_of_each_cut, dir_to_save, config)

def generate_final_video(config):
    totalCutsFound = 0
    generic_utils.create_functional_dir()
    start_time = dt.datetime.now()
    notification_system.notify_progress_bar(f"Iniciando em {get_datetime_without_milliseconds(start_time)}", 5)
    try:
        files = [os.path.join(config['videos_path_dir'], file) for file in os.listdir(config['videos_path_dir']) if os.path.isfile(os.path.join(config['videos_path_dir'], file))]
        if len(files) > 1:
            notification_system.notify_progress_bar(f"Mesclando os {len(files)} vídeos", 10)

        combined_videos = video_manipulation.merge_videos(files)
        (totalCutsFound, sum_seconds_total_video) = generate_cut_video(config, files, EXPORT_PATH, combined_videos)
        end_time = dt.datetime.now()
        processing_time = end_time - start_time
        minutes_difference = processing_time.seconds // 60
        seconds_difference = processing_time.seconds % 60
        finalLogMessage = f"Finalizando o processamento do vídeo em {get_datetime_without_milliseconds(end_time)}.\nTempo de processamento: {minutes_difference} minutos e {seconds_difference} segundos\nTotal de {len(files)} vídeos processados, com total de {totalCutsFound} cortes encontrados e {get_pretty_minutes(sum_seconds_total_video / 60)} minutos de vídeo."
        notification_system.notify(finalLogMessage)
        send_email(config, f"Vídeo {config['final_video_name']} processado", finalLogMessage)
    except Exception as e:
        send_email(config, f"Vídeo {config['final_video_name']} não processado", f"Erro de sistema {str(e)}")
        raise e
    