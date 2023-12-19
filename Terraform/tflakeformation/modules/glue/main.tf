
resource "aws_glue_crawler" "example_crawler" {
  name        = "example-crawler"
  database_name = "your_database_name"
  role_arn = var.role_arn

}

resource "aws_glue_crawler" "example_crawler" {
  name        = "example-crawler"
  database_name = "your_database_name"
  role_arn = var.role_arn

}
// Outras configurações do módulo Glue, se necessário
