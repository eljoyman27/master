from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime


def tarea_programada():
    print(f"Tarea ejecutada a las: {datetime.datetime.now().strftime('%H:%M:%S')}")


if __name__ == '__main__':
    # Inicializar el programador
    scheduler = BackgroundScheduler()

    # Programar la tarea para ejecutarse cada 10 segundos
    scheduler.add_job(tarea_programada, 'interval', seconds=10)

    # Iniciar el programador
    scheduler.start()
    print("Programador iniciado. Presiona Ctrl+C para salir.")

    try:
        # Mantener el programa principal vivo
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()