{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/scripts/verify.sh\" --hook"
          }
        ]
      }
    ]
  }
}
