from server import app, status_thread

if __name__ == "__main__":
    if not status_thread.is_alive():
        print('status thread running')
        status_thread.start()
        
    app.run()
