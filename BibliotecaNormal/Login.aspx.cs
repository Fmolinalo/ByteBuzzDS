using System;
using System.Linq;
using System.Web.UI;
using System.Web.Security;
using System.Data.Entity.Validation;
using BibliotecaNormal.Models;

namespace BibliotecaNormal
{
    public partial class Login : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            lblError.Visible = false;
        }

        protected void btnLogin_Click(object sender, EventArgs e)
        {
            string username = txtUsername.Text.Trim();
            string password = txtPassword.Text.Trim();

            using (var db = new BibliotecaDBEntities1())
            {
                var usuario = db.Usuario.FirstOrDefault(u => u.username == username && u.password_hash == password);

                if (usuario != null)
                {
                    FormsAuthentication.SetAuthCookie(username, chkRememberMe.Checked);

                    Response.Redirect("~/Dashboard.aspx");
                }
                else
                {
                    // La autenticación falló
                    lblError.Visible = true;
                }
            }
        }
    }
}
