import requests

def test_get_sidebar_data():
    url = 'http://localhost:8080/api/sidebar-data'
    response = requests.get(url)
    
    if response.status_code == 200:
        print('Success!')
        print('Response JSON:', response.json())
    else:
        print('Failed to get data')
        print('Status Code:', response.status_code)
        print('Response:', response.text)

if __name__ == "__main__":
    test_get_sidebar_data()
