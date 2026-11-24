import requests

def fectch_random_user_freeapi():
    url = "https://prod-main-api-704464-00tre1p1erm.compute.instacloud-edge.com/api/v1/public/randomusers/user/random"
    response = requests.get(url)
    data = response.json()


    if data["success"] and "data" in data:
        user_data = data["data"]
        name = (
            user_data["name"]["title"] + " " +
            user_data["name"]["first"] + " " +
            user_data["name"]["last"]
        )
        username = user_data["login"]["username"]
        country = user_data["location"]["country"]
        return name, username, country
    
def youtub_fetch_video():

    url = "https://prod-main-api-704464-00tre1p1erm.compute.instacloud-edge.com/api/v1/public/youtube/videos?page=1&limit=5"

    try:
        response = requests.get(url, timeout=(5, 15))

        response.raise_for_status()

        data = response.json()

        if not data.get("success"):
            print("API returned unsuccessful response")
            return []

        videos_data = data.get("data", {}).get("data", [])

        results = []

        for video in videos_data:
            video_details = video.get("items", {})
            snippet = video_details.get("snippet", {})

            video_id = video_details.get("id")
            title = snippet.get("title")

            if video_id and title:
                results.append({
                    "id": video_id,
                    "title": title
                })


            # print("video details ", video_details)
            print("video_id details ", video_id)
            print("title details ", title)




        # if data["success"] and "data" in data:
        #     videos = data["data"]["data"]
        #     print("data: ",data["data"]["data"][0])
        #     for video in videos:
        #         id = video["items"]["id"]
        #         title = video["items"]["snippet"]["title"]
        #         print(f"Id: {id},  Title: {title}")

    except requests.exceptions.Timeout:
        print("API request timed out")

    except requests.exceptions.HTTPError as e:
        print("HTTP error: %s", e)

    except requests.exceptions.RequestException as e:
        print("Request failed: %s", e)

    except ValueError as e:
        print("Invalid JSON response: %s", e)

    return []


youtub_fetch_video()


# def main():
#     try:
#         name, username, country = fectch_random_user_freeapi()
#         print(f"Name: {name} \nUsername: {username} \nCountry: {country}")
#     except Exception as e:
#         print("error ", str(e))

# if __name__ == "__main__":
#     main()