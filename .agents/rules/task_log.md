# Rule: End of Session Task Log Generation

Whenever the user indicates they are ending the session, wrapping up, or going to sleep (e.g., saying "I am going", "goodnight", "wrapping up for today"), the AI agent MUST automatically:

1. Update/generate the `TASK_LOG.md` file at the workspace root (`c:\Downloads\Blueshore-Technologies-main\TASK_LOG.md`).
2. Include:
   - What was accomplished in the current session (exact files modified, features added, bugs fixed).
   - What was accomplished in recent past sessions (context, server state, deployments).
   - The current architecture state, container statuses, and live URLs.
   - What tasks remain outstanding / what is left to do for future sessions.
3. Present a clear summary of the updated `TASK_LOG.md` to the user in the final response.
