tell application "Notes"
  set myFolder to first folder whose name = "memosearch"
  repeat with theNote in notes of myFolder
    set theNoteName to name of theNote
    log theNoteName

    set theNoteBody to body of theNote
    log theNoteBody

    log "[NOTE SEP]"
  end repeat
end tell
