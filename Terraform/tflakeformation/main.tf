
module "roles" {
  source = "./modules/roles"
  // Outras variáveis necessárias para o módulo roles
}

module "glue" {
  depends_on = [ module.roles]
  source = "./modules/glue"
  // Outras variáveis necessárias para o módulo Glue
  role_arn = module.roles.crawler_role_arn
}
