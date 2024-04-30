from flask import Flask, request, jsonify
from flask_cors import CORS
from query import processRequest
from pair_csv_to_json import csvToJson
from main import main
from filename_to_response import fileNameToResponse
import json
import time

app = Flask(__name__)
CORS(app)

@app.route("/", methods = ['POST', 'GET'])
def handleRequest():
    try:
      start = time.time()
      print(f'\n😀 {request.method} 요청도착! ')
      req = json.loads(request.args["data"])
      print(f'🎉 요청데이터: {req}')
      csvFiles = processRequest(req)
      print(f'🎉 csvFiles: {csvFiles}')
      pairNames, jsonFiles = csvToJson(csvFiles)
      print(f'🎉 pairNames: {pairNames}'
            f'\n🎉 jsonFiles: {jsonFiles}')
      topTwentyFileNames = main(pairNames, jsonFiles) #length is fourty (top twenty + simillar floor plan)
      print(f'🎉 topTwentyFileNames: {topTwentyFileNames}')
      data = fileNameToResponse(topTwentyFileNames)
      print(f'🎉 data: {data}')
      return jsonify({"status": 200, "message": f'time: {time.time() - start}s', "data": data})
    except:
      print("😱 예외발생")
      return jsonify({"status": 400, "message": "error occurred", "data": ""})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)