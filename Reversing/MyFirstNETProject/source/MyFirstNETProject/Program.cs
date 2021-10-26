using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;

namespace MyFirstNETProject
{
    class Program
    {

        static void Main(string[] YOIopllLQ)
        {
            string[] phrases = { "The river stole the gods.",
                                    "He picked up trash in his spare time to dump in his neighbor's yard.",
                                    "Little Red Riding Hood decided to wear orange today.",
                                    "He was sitting in a trash can with high street class.",
                                    "He put heat on the wound to see what would grow.",
                                    "She wasn't sure whether to be impressed or concerned that he folded underwear in neat little packages.",
                                    "The chic gangster liked to start the day with a pink scarf.",
                                    "The elephant didn't want to talk about the person in the room.",
                                    "She used her own hair in the soup to give it more flavor.",
                                    "If you really strain your ears, you can just about hear the sound of no one giving a damn.",
                                    "Seek success, but always be prepared for random cats.",
                                    "I love eating toasted cheese and tuna sandwiches.",
                                    "Flash photography is best used in full sunlight.",
                                    "He wasn't bitter that she had moved on but from the radish.",
                                    "Behind the window was a reflection that only instilled fear."};

            Random hGAXXQAqqq = new Random();

            if (YOIopllLQ.Contains("--FAWjasczxzz"))
            {
                string tHQHNNAA = Console.ReadLine();
                byte[] gxxx = { 113, 109, 168, 112, 209, 58, 221, 109, 155, 133, 249, 199, 54, 132, 226, 25 };
                byte[] QTQSss = { 137, 142, 36, 84, 16, 29, 199, 68, 117, 141, 232, 17, 95, 210, 173, 53 };
                byte[] hHVVaaaaQQ = { 63, 82, 240, 53, 7, 254, 188, 80, 248, 35, 173, 171, 8, 50, 91, 91, 218, 84, 5, 62, 92, 56, 189, 60, 43, 98, 3, 110, 19, 128, 82, 125 };
                byte[] DAnqamma = { 43, 12, 65, 21, 76, 12, 54, 98, 34, 121, 233, 152, 76, 11, 43, 12, 76 };
                byte[] GnQNAA = { 21, 36, 52, 19, 53, 85, 58, 95, 29, 34, 10, 55, 106, 126, 60, 49, 38, 121, 48, 11, 119, 54, 37, 1, 119, 8, 75, 4, 113, 48, 76, 73, 0, 126, 33, 60, 11, 122, 78, 31 };
                byte[] Bnmmm = { 231, 195, 94, 214, 206, 204, 92, 198, 251, 231, 114, 240, 238, 241, 126, 192, 238, 245, 80, 203, 199, 240, 89, 192, 216, 230, 107, 233, 229, 222, 123, 246, 235 };
                byte[] NHAAqq = { 192, 43, 85, 204, 216, 101, 194, 44, 75, 228, 224, 78, 231, 105, 115, 251 };
                // Encrypt the string to an array of bytes.
                try
                {
                    byte[] jhs = PTKQNxlAmQQQ(tHQHNNAA, gxxx, QTQSss);

                    if (NHAAqq.Equals(Bnmmm) && DAnqamma.Length > 0x43)
                    {
                        for (int hehjasaaa = 0; hehjasaaa < GnQNAA.Length; hehjasaaa++)
                        {
                            Console.Write(Convert.ToChar(NHAAqq[hehjasaaa] ^ tHQHNNAA[hehjasaaa % GnQNAA.Length]));
                        }
                    }
                    if (jhs.SequenceEqual(hHVVaaaaQQ) && 432 > QTQSss.Length && hGAXXQAqqq.Next(0, NHAAqq.Length) > 0x1289)
                    {
                        for (int ggrwe = 0; ggrwe < GnQNAA.Length; ggrwe++)
                        {
                            Console.Write(Convert.ToChar(GnQNAA[ggrwe] ^ tHQHNNAA[ggrwe % tHQHNNAA.Length]));
                        }
                    }
                }
                catch
                {
                }
            }

            Console.WriteLine(phrases[hGAXXQAqqq.Next(0, phrases.Length)]);
            Console.ReadLine();
        }

        static byte[] PTKQNxlAmQQQ(string HNNNnacxXXxz, byte[] hBTQQQQ, byte[] FNFNnanAAA)
        {
            // Check arguments.
            if (HNNNnacxXXxz == null || HNNNnacxXXxz.Length <= 0 || hBTQQQQ == null || hBTQQQQ.Length <= 0 || FNFNnanAAA == null || FNFNnanAAA.Length <= 0)
                throw new Exception();

            byte[] FnbhaDqqqq;

            // Create an Aes object
            // with the specified key and IV.
            using (Aes fHaQjTAf = Aes.Create())
            {
                fHaQjTAf.Key = hBTQQQQ;
                fHaQjTAf.IV = FNFNnanAAA;
                fHaQjTAf.Mode = CipherMode.ECB;

                // Create an encryptor to perform the stream transform.
                ICryptoTransform gFBGaqqq = fHaQjTAf.CreateEncryptor(fHaQjTAf.Key, fHaQjTAf.IV);

                // Create the streams used for encryption.
                using (MemoryStream GAWcccAAqq = new MemoryStream())
                {
                    using (CryptoStream GHSadssAAAA = new CryptoStream(GAWcccAAqq, gFBGaqqq, CryptoStreamMode.Write))
                    {
                        using (StreamWriter IUYmwmlfagq = new StreamWriter(GHSadssAAAA))
                        {
                            //Write all data to the stream.
                            IUYmwmlfagq.Write(HNNNnacxXXxz);
                        }
                        FnbhaDqqqq = GAWcccAAqq.ToArray();
                    }
                }
            }

            // Return the encrypted bytes from the memory stream.
            return FnbhaDqqqq;
        }
    }
}
