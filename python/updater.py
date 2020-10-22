# import
import os
import json
import pathlib

filename = os.getenv("label") or "test"
content = os.getenv("content") or "content"

root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / f"config/{filename}.json", 'r+') as filehandle:
    data = json.load(filehandle)
    print(data)
    data.append(f"{content.rstrip()}")
    filehandle.seek(0)
    json.dump(data, filehandle, indent=4)