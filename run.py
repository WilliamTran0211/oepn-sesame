import uvicorn
import multiprocessing


def run_rest():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    rest_process = multiprocessing.Process(target=run_rest)
    rest_process.start()
    rest_process.join()
