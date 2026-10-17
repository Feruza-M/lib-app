output "instance_id" {
  value = aws_instance.lib_app.id
}

output "public_ip" {
  value = aws_instance.lib_app.public_ip
}

output "private_ip" {
  value = aws_instance.lib_app.private_ip
}
