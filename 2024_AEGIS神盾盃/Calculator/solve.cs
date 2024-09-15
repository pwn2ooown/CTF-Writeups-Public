using System;

using System.Text;

public class HelloWorld

{

    public static void Main(string[] args)

    {
        // 打開 DNSPY 就有這串可疑的 check 就是 flag checker
        string text3 = "1565023222387235312162663";

	string text4 = string.Format("{0}", (long.Parse(text3.Substring(0, 5)) ^ 56L) + 65681531L) + string.Format("{0}", (long.Parse(text3.Substring(5, 4)) ^ 8L) + 83121454L) + string.Format("{0}", (long.Parse(text3.Substring(9, 8)) ^ 56L) + 65681531L) + string.Format("{0}", (long.Parse(text3.Substring(17, 8)) ^ 8L) + 83121454L);

        Console.WriteLine ("{0}",text4);

        int[] array = new int[]

		{

			2, 2, 2, 2, 2, 3, 2, 2, 2, 2,

			2, 2, 2, 2, 3

		};

		StringBuilder stringBuilder = new StringBuilder();

		int num = 0;

		foreach (int num2 in array)

		{

			string text5 = text4.Substring(num, num2);

			int num3 = int.Parse(text5);

			char c = (char)num3;

			stringBuilder.Append(c);

			num += num2;

		}

		Console.WriteLine ("{0}",stringBuilder);

    }

}