import threading
import time

currentBandwidth = 0
lock = threading.Lock()

def allocateBandwidth(user_id):
    global currentBandwidth
    flag = True
    while flag:
        time.sleep(0.5)
        lock.acquire()
        if currentBandwidth < 20:
            try:
                currentBandwidth += 1
                print(f"User {user_id} is downloading => Current Bandwidth : {currentBandwidth} MB")
            except:
                print('an error occured')
            finally:
                lock.release()
                
            time.sleep(1)

            try:
                lock.acquire()
                currentBandwidth -= 1
                print(f"{user_id} finish download => Current Bandwidth : {currentBandwidth} MB")
            except:
                print('an error occured')
            finally:
                lock.release()
                flag = False
        else:
            print(f"{user_id} is waiting => Current bandwidth : {currentBandwidth} MB")
            lock.release()


if __name__ == '__main__':

    users = []
    for i in range(50):
        user = threading.Thread(target=allocateBandwidth, args=(i,))
        users.append(user)
        user.start()

    for user in users:
        user.join()