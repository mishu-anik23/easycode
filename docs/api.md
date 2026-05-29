# API Documentation

## POST /chat
- Request: `project_id`, `message`, `selected_files`, `mode`
- Response: `reply`, `used_context`, `tokens`

## POST /plan
- Request: `project_id`, `goal`
- Response: `steps`

## POST /diff
- Request: `project_id`, `goal`, `files`
- Response: `diff`

## POST /apply
- Request: `project_id`, `diff`
- Response: `status`

## POST /index
- Request: `project_path`
- Response: `status`, `files`

## POST /search
- Request: `project_id`, `query`
- Response: `results`
