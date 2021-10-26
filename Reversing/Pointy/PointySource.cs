//Solution: open with dnspy
//Make: install visual studio or don't if you want to save 80gb and 9 years of your life
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Pointy
{
    class Program
    {
        static void Main(string[] args)
        {
            string flag = "WMG{b0r1n6_e45y_r3v3r51ng}";
            Console.Write("Enter password: ");
            string username = Console.ReadLine();
            Console.WriteLine("Invalid password");
            string something = flag + username;
        }
    }
}
