output "api_endpoint" {
  description = "HTTP API endpoint"
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}

output "lambda_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.handler.function_name
}
