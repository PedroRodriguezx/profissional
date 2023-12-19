provider "aws" {
  alias  = "central"
  region = "us-east-1"  # Defina a região AWS desejada
}


# Passo 1: Criação da Role
resource "aws_iam_role" "s3_replication_role" {
  name = "S3ReplicationRole"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}
# Passo 2: Criação da Policy
resource "aws_iam_policy" "s3_replication_policy" {
  name        = "S3ReplicationPolicy"
  description = "Policy for S3 replication"
  
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:ListBucket",
        "s3:GetReplicationConfiguration",
        "s3:GetObjectVersionForReplication",
        "s3:GetObjectVersionAcl",
        "s3:GetObjectVersionTagging",
        "s3:GetObjectRetention",
        "s3:GetObjectLegalHold"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::${var.SourceBucketName}",
        "arn:aws:s3:::${var.SourceBucketName}/*",
        "arn:aws:s3:::${var.TargetBucketName}",
        "arn:aws:s3:::${var.TargetBucketName}/*"
      ]
    },
    {
      "Action": [
        "s3:ReplicateObject",
        "s3:ReplicateDelete",
        "s3:ReplicateTags",
        "s3:ObjectOwnerOverrideToBucketOwner"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::${var.SourceBucketName}/*",
        "arn:aws:s3:::${var.TargetBucketName}/*"
      ]
    }
  ]
}
EOF
}

# Passo 3: Attachment da Policy na Role
resource "aws_iam_role_policy_attachment" "s3_replication_attachment" {
  policy_arn = aws_iam_policy.s3_replication_policy.arn
  role       = aws_iam_role.s3_replication_role.name
}


resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = var.SourceBucketName
  versioning_configuration {
    status = "Enabled"
  }
}


resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.central
  # Must have bucket versioning enabled first
  role   = aws_iam_role.s3_replication_role.arn
  bucket = var.SourceBucketName
  rule {
    id = "Rule1"
    status = "Enabled"
    destination {
      bucket        = "arn:aws:s3:::${var.TargetBucketName}/*"
      storage_class = "STANDARD"
    }
  }
}

