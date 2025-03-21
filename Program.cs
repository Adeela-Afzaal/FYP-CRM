// File: Program.cs
using BlazorApp_Meta_UI;
using BlazorApp_Meta_UI.Services;
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using System.Net.Http;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

// Set up HttpClient with FastAPI server address
builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri("http://127.0.0.1:8000/") });
builder.Services.AddScoped<ApiService>();
builder.Services.AddScoped<ScheduleService>();
builder.Services.AddSingleton<TaskService>();
builder.Services.AddScoped<Authentication>();
builder.Services.AddScoped<MessageService>();




await builder.Build().RunAsync();
