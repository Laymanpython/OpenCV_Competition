using System;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class PAI : Form
    {
        //public static Form1 form = new Form1();
        Form1 _form1;


        public PAI(Form1 form1)
        {
            InitializeComponent();

            _form1 = form1;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //form.Show();

        }

        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            linkLabel1.LinkVisited = true;
            _form1.Show();
            this.Hide();
        }
    }
}
