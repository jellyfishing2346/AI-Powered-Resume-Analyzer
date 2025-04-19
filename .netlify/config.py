{
  "build": {
    "environment": {
      "AWS_LAMBDA_JS_RUNTIME": "nodejs20.x"
    }
  },
  "plugins": [
    {
      "package": "@netlify/plugin-cache",
      "config": {
        "paths": [
          "venv",
          ".cache/pip",
          "node_modules"
        ]
      }
    }
  ]
}