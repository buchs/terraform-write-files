variable "files" {
  type = "map"
}

data "external" "write_files" {
  program = ["python3", "${path.module}/write-files.py"]
  query   = var.files
}
