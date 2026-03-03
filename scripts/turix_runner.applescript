-- TuriXRunner: stable GUI host for ScreenCapture permissions
-- Usage:
--   open -a TuriXRunner --args "Open Safari and go to github.com"
-- If no args provided, it will prompt.

on run argv
	set taskText to ""
	if (count of argv) > 0 then
		set taskText to item 1 of argv
	else
		display dialog "What should TuriX do?" default answer "Open Safari and go to github.com" buttons {"Cancel", "Run"} default button "Run"
		set taskText to text returned of result
	end if

	-- shell wrapper: loads API key from Keychain (if present) and runs the turix-cua skill script
	set sh to "set -e; " & ¬
		"export PATH=\"/Users/mac/miniconda3/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:\\$PATH\"; " & ¬
		"API_KEY=\"$(security find-generic-password -a \\\"$USER\\\" -s turix_dashscope_api_key -w 2>/dev/null || true)\"; " & ¬
		"if [ -n \"$API_KEY\" ]; then export API_KEY; fi; " & ¬
		"bash /Users/mac/.openclaw/skills/turix-cua/scripts/run_turix.sh " & quoted form of taskText

	-- Run via do shell script (no Terminal Apple Events needed). Log to file.
	set logFile to "/Users/mac/.openclaw/logs/turix_runner.log"
	set sh2 to sh & " >> " & quoted form of logFile & " 2>&1 &"
	do shell script sh2
	display notification "Task launched: " & taskText with title "TuriXRunner"
end run
