using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Text;

namespace Examples.System.Net {
    public class WebRequestPostExample {
        public static void Main() {
            // "Starts" http client
            var client = new HttpClient();

            // Login
            var data = new Dictionary<string, string>();
            data.Add("username", "andre.aragao");
            data.Add("password", "Dufwine#1003");
            NewPost("http://127.0.0.1:8000/game-login/", data, client);

            // Match register
            var data2 = new Dictionary<string, string>();
            data2.Add("role", "Scrum Master");
            data2.Add("hits", "10");
            data2.Add("mistakes", "2");
            data2.Add("individual_feedback", "Muito bom!");
            data2.Add("group", "Tigers");
            NewPost("http://127.0.0.1:8000/match-register/", data2, client);
        }

        // NewPost is the way recommended by Micrsoft
        public static void NewPost(string url, Dictionary<string, string> data, HttpClient client) {
            var req = new HttpRequestMessage(HttpMethod.Post, url) { Content = new FormUrlEncodedContent(data) };
            client.SendAsync(req).Wait();
        }

        public static void Post(string url, string postData) {
            // Create a request using a URL that can receive a post.
            WebRequest request = WebRequest.Create(url);
            // Set the Method property of the request to POST.
            request.Method = "POST";

            // Create POST data and convert it to a byte array. Ex: "name=BondeDoTigrao&score=0"
            byte[] byteArray = Encoding.UTF8.GetBytes(postData);

            // Set the ContentType property of the WebRequest.
            request.ContentType = "application/x-www-form-urlencoded";
            // Set the ContentLength property of the WebRequest.
            request.ContentLength = byteArray.Length;

            // Get the request stream.
            Stream dataStream = request.GetRequestStream();
            // Write the data to the request stream.
            dataStream.Write(byteArray, 0, byteArray.Length);
            // Close the Stream object.
            dataStream.Close();

            // Get the response.
            WebResponse response = request.GetResponse();
            // Display the status.
            Console.WriteLine(((HttpWebResponse)response).StatusDescription);

            // Get the stream containing content returned by the server.
            // The using block ensures the stream is automatically closed.
            using(dataStream = response.GetResponseStream()) {
                // Open the stream using a StreamReader for easy access.
                StreamReader reader = new StreamReader(dataStream);
                // Read the content.
                string responseFromServer = reader.ReadToEnd();
                // Display the content.
                Console.WriteLine(responseFromServer);
            }

            // Close the response.
            response.Close();
        }
    }
}