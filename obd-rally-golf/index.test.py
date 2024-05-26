from firebase.Firebase import Firebase
import os

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"

fb = Firebase()

# get data from original firesttore
# fb.fetch_data_document('vova')

# enable emulator and run this command to set from file
# fb.overwrite_document('/Users/vo1/Developer/github.com/vosamoilenko/race-monitor-x-pro/vova.json', 'vova')

