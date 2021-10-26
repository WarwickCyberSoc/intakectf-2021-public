package decaf;

import java.util.Scanner;

public class Main {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter exit to exit the program");
        String userInput ="";
        while(!userInput.equals("exit")){
            System.out.printf("Enter word: ");
            userInput = sc.nextLine();
            System.out.printf("You said '%s'!%n",userInput);
            int i = 4;
            if (i==3){
            	gf();
            }
        }
        System.out.println("Exiting");
        sc.close();

    }

    public static void gf(){
    	System.out.print("WMG{");
    	System.out.println((new Object() {int t;public String toString() {byte[] buf = new byte[37];t = -915745722;buf[0] = (byte) (t >>> 16);t = -983655842;buf[1] = (byte) (t >>> 7);t = 1371216811;buf[2] = (byte) (t >>> 15);t = 1637949736;buf[3] = (byte) (t >>> 19);t = -521185344;buf[4] = (byte) (t >>> 6);t = 1735850909;buf[5] = (byte) (t >>> 3);t = 1915181698;buf[6] = (byte) (t >>> 12);t = 416750515;buf[7] = (byte) (t >>> 22);t = 2094249653;buf[8] = (byte) (t >>> 4);t = 163640791;buf[9] = (byte) (t >>> 9);t = 1447280936;buf[10] = (byte) (t >>> 17);t = 1739980471;buf[11] = (byte) (t >>> 12);t = 2010269321;buf[12] = (byte) (t >>> 24);t = 1720221273;buf[13] = (byte) (t >>> 20);t = -677653061;buf[14] = (byte) (t >>> 20);t = 978108166;buf[15] = (byte) (t >>> 9);t = 589903030;buf[16] = (byte) (t >>> 8);t = 960582756;buf[17] = (byte) (t >>> 23);t = 1883276095;buf[18] = (byte) (t >>> 4);t = -1976991805;buf[19] = (byte) (t >>> 10);t = -1982842648;buf[20] = (byte) (t >>> 18);t = 1262826934;buf[21] = (byte) (t >>> 19);t = 1675461017;buf[22] = (byte) (t >>> 3);t = 2139906022;buf[23] = (byte) (t >>> 8);t = 476800751;buf[24] = (byte) (t >>> 11);t = -1181159902;buf[25] = (byte) (t >>> 15);t = 460590404;buf[26] = (byte) (t >>> 19);t = 1092144569;buf[27] = (byte) (t >>> 10);t = -1368712175;buf[28] = (byte) (t >>> 21);t = -1718102517;buf[29] = (byte) (t >>> 14);t = -999102896;buf[30] = (byte) (t >>> 9);t = -1184184803;buf[31] = (byte) (t >>> 5);t = -1583878523;buf[32] = (byte) (t >>> 14);t = -2067558163;buf[33] = (byte) (t >>> 20);t = 233919470;buf[34] = (byte) (t >>> 21);t = 929744710;buf[35] = (byte) (t >>> 23);t = 949494776;buf[36] = (byte) (t >>> 7);return new String(buf);}}.toString()));
    	System.out.println("}");
    }

}
