from supabase import create_client
supabase = create_client("https://aynxwbozwlftwurmylkv.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF5bnh3Ym96d2xmdHd1cm15bGt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5ODgwMTUsImV4cCI6MjA3NDU2NDAxNX0.ofjt6mDxwW7HZjXce3gq4-4kXxQRYtV0GGOXo-QTXGE")
response = supabase.table("raw_data").select("*").execute()
print(response.data)  # 應返回空列表（新表）