provider "aws" {
}

variable "table_name" {
  type = string
  description = "DynamoDB tableName variable"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name        = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key       = "patientId"
  attribute {
    name = "patientId"
    type = "S"
  }
   tags = {
    environment       = "dev"
  }
}

output "dynamodb_arn" {
  value = aws_dynamodb_table.basic-dynamodb-table.arn
  description = "DynamoDB ARN"
}
