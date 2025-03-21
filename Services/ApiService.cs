using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace BlazorApp_Meta_UI.Services
{
    public class ApiService
    {
        private readonly HttpClient _httpClient;

        public ApiService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<string> PostTextToFacebook(string message)
        {
            var content = new MultipartFormDataContent();
            content.Add(new StringContent(message), "message");

            var response = await _httpClient.PostAsync("post_text_to_facebook", content);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }

        public async Task<string> PostImageToFacebook(byte[] imageData, string caption)
        {
            using var content = new MultipartFormDataContent();
            // Make sure to use the key "file" to match the FastAPI endpoint
            content.Add(new ByteArrayContent(imageData), "file", "upload.jpg");
            // Use the key "caption" for the caption
            content.Add(new StringContent(caption), "caption");

            var response = await _httpClient.PostAsync("http://127.0.0.1:8000/post_image_to_facebook", content);
            response.EnsureSuccessStatusCode();  // This will throw if the status code is not 2xx
            return await response.Content.ReadAsStringAsync();
        }
        // Send a custom message to Facebook Messenger/Instagram
        public async Task<string> SendMessageToRecipient(string recipientId, string message)
        {
            var content = new MultipartFormDataContent();
            content.Add(new StringContent(recipientId), "psid");
            content.Add(new StringContent(message), "message");

            var response = await _httpClient.PostAsync("http://127.0.0.1:8000/send_message", content);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
    }
}