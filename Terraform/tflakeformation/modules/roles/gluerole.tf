resource "aws_iam_role" "crawler_role" {
  name = "crawler_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "glue.amazonaws.com"  # Permite ao Glue assumir esta role
        }
      }
    ]
  })
}

resource "aws_iam_policy" "crawler_policy" {
  name        = "crawler_policy"
  description = "Política para o Glue Crawler"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "VisualEditor0",
        Effect = "Allow",
        Action = [
          "glue:BatchCreatePartition",
          "glue:GetDatabase",
          "cloudwatch:PutMetricData",
          "glue:CreateTable",
          "glue:GetTables",
          "glue:GetTableVersions",
          "glue:GetPartitions",
          "glue:CreateDatabase",
          "glue:UpdateTable",
          "glue:GetTable",
          "glue:BatchGetPartition",
          "glue:UpdatePartition",
          "s3:PutObject",
          "s3:GetObject",
          "logs:CreateLogStream",
          "s3:DeleteObject",
          "logs:CreateLogGroup",
          "logs:PutLogEvents",
        ],
        Resource = [
          "*",
          "arn:aws:logs:*:*:/aws-glue/*",
          "arn:aws:logs:*:*:/customlogs/*",
          "arn:aws:s3:::json-source-bucket/*",
          "arn:aws:s3:::parquet-target-bucket-test/*",
        ],
      },
      {
        Sid    = "LakeFormationDataAccess",
        Effect = "Allow",
        Action = ["lakeformation:GetDataAccess"],
        Resource = "*",
      },
    ],
  })
}

resource "aws_iam_policy_attachment" "crawler_role_attachment" {
  depends_on = [ aws_iam_role.crawler_role, aws_iam_policy.crawler_policy ]
  policy_arn = aws_iam_policy.crawler_policy.arn
  roles      = [aws_iam_role.crawler_role.name]
}
