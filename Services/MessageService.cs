using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
namespace BlazorApp_Meta_UI.Services
{
    using System.Net.Http;
    using System.Net.Http.Json;
    using System.Threading.Tasks;

    public class MessageService
    {
        private readonly HttpClient _httpClient;

        public MessageService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<Message>> GetMessagesAsync()
        {
            var response = await _httpClient.GetFromJsonAsync<ApiResponse>("/api/facebook/messages");
            return response?.Messages ?? new List<Message>();
        }
    }

    public class ApiResponse
    {
        public List<Message>? Messages { get; set; }
    }

    public class Message
    {
        public string? SenderId { get; set; }

        public string? MessageText { get; set; }
        public double Timestamp { get; set; }
    }

}