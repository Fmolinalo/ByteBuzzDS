using System;
using System.Linq;
using System.Web.UI;
using BibliotecaNormal.Models;

namespace BibliotecaNormal
{
    public partial class Dashboard : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                // Leer el parámetro de la URL para determinar qué panel mostrar
                string page = Request.QueryString["page"];
                if (string.IsNullOrEmpty(page))
                {
                    page = "dashboard"; // Por defecto, mostrar el dashboard
                }
            }
        }
    }
}
