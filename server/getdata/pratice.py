

def get_request_url(method='/movie/popular', **kwargs):
    """API 요청에 필요한 주소를 구성합니다.
    
    Args:
        method: API 서비스에서 제공하는 메서드로써 기본 경로 뒤에 추가됩니다.
        **kwargs: 쿼리 스트링 형태로 기본 요청 주소 뒤에 추가됩니다.

    Returns:
        base_url, 메서드, 쿼리 스트링으로 구성된 요청 주소를 반환합니다.
    """
    base_url = 'https://api.themoviedb.org/3'
    request_url = base_url + method
    request_url += f'?api_key={api_key}'

    for k, v in kwargs.items():
        request_url += f'&{k}={v}'

    return request_url

credits_url = get_request_url(method=f'/movie/{movie_list_id[i]}/keyword', region='KR', language='ko')
    #print(credits_url)
    credits_list = requests.get(credits_url).json()