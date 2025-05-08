import requests
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from .serializer import PostSerializer

AI_SERVICE_URL = "http://127.0.0.1:8001/generate-post/"  # Replace with the correct AI service URL

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter posts by the logged-in user
        return Post.objects.filter(author=self.request.user).order_by("-published_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set the author field to the logged-in user

    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)  # Log the incoming request data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation Errors:", serializer.errors)  # Log validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def generate_post_from_explanation(request):
    if request.method == "POST":
        # Get the explanation from the request body
        explanation = request.data.get('explanation')  # Use request.data for consistency with DRF

        if not explanation:
            return JsonResponse({"error": "Explanation is required"}, status=400)

        # Send the explanation to the FastAPI service
        try:
            response = requests.post(AI_SERVICE_URL, json={"explanation": explanation})
            response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)

            # Parse the response from FastAPI
            generated_post = response.json().get('generated_post')
            if not generated_post:
                return JsonResponse({"error": "Invalid response from AI service"}, status=500)

            # Create the post in the database with the current logged-in user as author
            post = Post.objects.create(
                author=request.user,  # Use the authenticated user from the request
                title=generated_post["title"],
                category=generated_post["category"],
                summary=generated_post["summary"],
                content=generated_post["content"],
                image_url=generated_post["image_url"],
                tags=generated_post["tags"],
                views=generated_post["views"],
                is_published=generated_post["is_published"],
                published_at=generated_post["published_at"],
                updated_at=generated_post["updated_at"],
                target_branches=generated_post["target_branches"],
                target_years=generated_post["target_years"],
            )

            return JsonResponse({"message": "Post generated successfully", "post_id": post.id})

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Failed to generate post: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def proxy_generate_post(request):
    if request.method == "POST":
        try:
            # Forward the request to the FastAPI service
            response = requests.post("http://127.0.0.1:8001/generate-post/", json=request.POST)
            return JsonResponse(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
