using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Windows.Forms;
using System.IO;
using Microsoft.ML.OnnxRuntime.Tensors;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Processing;
using SixLabors.ImageSharp.PixelFormats;
using Microsoft.ML.OnnxRuntime;


namespace WindowsFormsApp1
{
    public partial class Xray : Form
    {
        Form1 _form1;


        public Xray(Form1 form1)
        {
            InitializeComponent();

            _form1 = form1;
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void Xray_Load(object sender, EventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            separation sep = new separation();
            string score = processing_score();
            string Tag = processing();
            string filename = sep.Separate();
            string[] names = filename.Split('_');
            string name = names[0];
            string IDnumber = names[1];
            string gender = names[2];
            string[] genders = gender.Split('.');
            gender = genders[0];
            if (String.Compare(gender, "M") == 0||String.Compare(gender,"m")==0)
            {
                gender = "男";
            }
            else
            {
                gender = "女";
            }
            textBox1.Text = score;
           // textBox4.Text = gender;
           // textBox3.Text = IDnumber;
            textBox3.Text = Tag;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            System.Threading.Thread s = new System.Threading.Thread(new System.Threading.ThreadStart(Getpicture));
            
            s.ApartmentState = System.Threading.ApartmentState.STA;
            s.Start(); 

        }


        private void Getpicture()
        {
            //string path = System.AppDomain.CurrentDomain.BaseDirectory;
            OpenFileDialog ofd = new OpenFileDialog();
            //ofd.InitialDirectory = @"D:/";
            ofd.Filter = "jpeg文件(*.jpg)|*.jpg|png文件(*.png)|*.png";
            ofd.FilterIndex = 1;
            ofd.RestoreDirectory = true;
            ofd.Title = "选择X光胸片";
            string path;
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                path = ofd.FileName;
                string pathname = System.AppDomain.CurrentDomain.BaseDirectory;
                using (Stream stream = ofd.OpenFile())
                {
                    using (FileStream fs = new FileStream(pathname + "张三_114514_M.jpg", FileMode.OpenOrCreate, FileAccess.ReadWrite))
                    {
                        stream.CopyTo(fs);
                        fs.Flush();
                    }
                }
                this.pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
                pictureBox1.Image = System.Drawing.Image.FromFile(path);
            }
            string imageFilePath = @"张三_114514_M.jpg";
            // Read image
            // Rgb24：Pixel type containing three 8-bit unsigned normalized values ranging from 0 to
            //        255. The color components are stored in red, green, blue order
            // SixLabors.ImageSharp.Image
        }

        private string processing()
        {
            string modelFilePath = @"D:\Assistant\WindowsFormsApp1\home.onnx";
            separation sep = new separation();
            string filename = sep.Separate();
            string imageFilePath = System.AppDomain.CurrentDomain.BaseDirectory + filename;
            using Image<Rgb24> image = SixLabors.ImageSharp.Image.Load<Rgb24>(imageFilePath);  // 以rgb形式读取图片
                                                                                               // Resize image
                                                                                               // Resize image
            image.Mutate(x =>
            {
                x.Resize(new ResizeOptions
                {
                    Size = new SixLabors.ImageSharp.Size(224, 224),
                    Mode = ResizeMode.Crop
                });
            });

            image.Mutate(x =>
                    x.Resize(224, 224)
            );


            // Preprocess image

            Tensor<float> input = new DenseTensor<float>(new[] { 1, 3, 224, 224 });
            var mean = new[] { 0.485f, 0.456f, 0.406f };
            var stddev = new[] { 0.229f, 0.224f, 0.225f };
            for (int y = 0; y < 224; y++)
            {
                image.ProcessPixelRows(im =>
                {
                    var pixelSpan = im.GetRowSpan(y);
                    for (int x = 0; x < 224; x++)
                    {
                        input[0, 0, y, x] = pixelSpan[x].R / 255f;
                        input[0, 1, y, x] = pixelSpan[x].G / 255f;
                        input[0, 2, y, x] = pixelSpan[x].B / 255f;
                    }
                });

            }



            // Setup inputs
            var inputs = new List<NamedOnnxValue>
            {
               NamedOnnxValue.CreateFromTensor("image", input)
            };

            // Run inference
            using var session = new InferenceSession(modelFilePath);
            using IDisposableReadOnlyCollection<DisposableNamedOnnxValue> results = session.Run(inputs);

            // Postprocess to get softmax vector
            IEnumerable<float> output = results.First().AsEnumerable<float>();  // First(): The first element in the specified sequence. AsEnumerable：
            float sum = output.Sum(x => (float)Math.Exp(x));   // sum(e^x)
            IEnumerable<float> softmax = output.Select(x => (float)Math.Exp(x) / sum);  // e^x / sum

            //Extract top 1 predicted classes
            IEnumerable<Prediction> top1 = softmax.Select((x, i) => new Prediction { Label = LabelMap.Labels[i], Confidence = x })
            .OrderByDescending(x => x.Confidence)
            .Take(1);
            string Tag = "none";
            foreach (var t in top1)
            {
                string c = t.Label;
                Tag = c;
            }
            
            return Tag;
        }

        private string processing_score()
        {
            string modelFilePath = @"D:\Assistant\WindowsFormsApp1\home.onnx";
            separation sep = new separation();
            string filename = sep.Separate();
            string imageFilePath = System.AppDomain.CurrentDomain.BaseDirectory + filename;
            using Image<Rgb24> image = SixLabors.ImageSharp.Image.Load<Rgb24>(imageFilePath);  // 以rgb形式读取图片
                                                                                               // Resize image
                                                                                               // Resize image
            image.Mutate(x =>
            {
                x.Resize(new ResizeOptions
                {
                    Size = new SixLabors.ImageSharp.Size(224, 224),
                    Mode = ResizeMode.Crop
                });
            });

            image.Mutate(x =>
                    x.Resize(224, 224)
            );


            // Preprocess image

            Tensor<float> input = new DenseTensor<float>(new[] { 1, 3, 224, 224 });
            var mean = new[] { 0.485f, 0.456f, 0.406f };
            var stddev = new[] { 0.229f, 0.224f, 0.225f };
            for (int y = 0; y < 224; y++)
            {
                image.ProcessPixelRows(im =>
                {
                    var pixelSpan = im.GetRowSpan(y);
                    for (int x = 0; x < 224; x++)
                    {
                        input[0, 0, y, x] = pixelSpan[x].R / 255f;
                        input[0, 1, y, x] = pixelSpan[x].G / 255f;
                        input[0, 2, y, x] = pixelSpan[x].B / 255f;
                    }
                });

            }



            // Setup inputs
            var inputs = new List<NamedOnnxValue>
            {
               NamedOnnxValue.CreateFromTensor("image", input)
            };

            // Run inference
            using var session = new InferenceSession(modelFilePath);
            using IDisposableReadOnlyCollection<DisposableNamedOnnxValue> results = session.Run(inputs);

            // Postprocess to get softmax vector
            IEnumerable<float> output = results.First().AsEnumerable<float>();  // First(): The first element in the specified sequence. AsEnumerable：
            float sum = output.Sum(x => (float)Math.Exp(x));   // sum(e^x)
            IEnumerable<float> softmax = output.Select(x => (float)Math.Exp(x) / sum);  // e^x / sum

            //Extract top 1 predicted classes
            IEnumerable<Prediction> top1 = softmax.Select((x, i) => new Prediction { Label = LabelMap.Labels[i], Confidence = x })
            .OrderByDescending(x => x.Confidence)
            .Take(1);
            string Tag = "none";
            foreach (var t in top1)
            {
                string c = t.Confidence.ToString();
                Tag = c;
            }

            return Tag;
        }

        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            linkLabel1.LinkVisited = true;
            _form1.Show();
            this.Hide();
        }
    }
    public class Prediction
        {
            public string Label { set; get; }
            public float Confidence { set; get; }
        }
        public static class LabelMap
        {
            static LabelMap()
            {
                Labels = new string[]
                {
            "新冠患者","病毒性肺炎","正常"
                };
            }

            public static string[] Labels { set; get; }


           
        }
    public class separation
    {
        public string Separate()
        {
            string path = System.AppDomain.CurrentDomain.BaseDirectory;
            var files = Directory.GetFiles(path, "*.jpg");
            string filen = files[0];
            string filename = Path.GetFileName(filen);//张三_114514_M.jpg
            return filename;
        }
    }
   // private static void pictureBox1_Click(object sender, EventArgs e)
   // {

   // }
        //private void textBox2_TextChanged(object sender, EventArgs e)
   // {

  //  }
    }
