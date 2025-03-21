using System.Net.Http.Json;
using System.Threading.Tasks;
using BlazorApp_Meta_UI.Pages;
using BlazorApp_Meta_UI.Models;

namespace BlazorApp_Meta_UI.Services
{
    public class Authentication
    {
        private readonly HttpClient _httpClient;

        public Authentication(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<bool> SignUpAsync(SignUpRequest model)
        {
            var response = await _httpClient.PostAsJsonAsync("http://localhost:8000/signup", model);

            if (response.IsSuccessStatusCode)
            {
                return true;
            }
            else
            {
                var error = await response.Content.ReadAsStringAsync();
                return false;
            }
        }

        public async Task<bool> LoginAsync(LoginModel model)
        {
            var response = await _httpClient.PostAsJsonAsync("http://localhost:8000/login", model);

            if (response.IsSuccessStatusCode)
            {
                return true;
            }
            else
            {
                var error = await response.Content.ReadAsStringAsync();
                return false;
            }
        }
    }
}
