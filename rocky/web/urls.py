
from django.urls import path
from . import views


urlpatterns = [
    # Public pages
    path("", views.index, name="index"),
<<<<<<< HEAD
    path("about", views.About, name="About"),
    path("projects", views.Projects, name="Projects"),
    path("contact", views.contact, name="contact"),
    path("dashboard/", views.dashboard_home, name="dashboard_home"), 
    path("dashboard/add/", views.add_project, name="add_project"), 
    path("dashboard/edit/<int:pk>/", views.edit_project, name="edit_project"), 
    path("dashboard/delete/<int:pk>/", views.delete_project, name="delete_project"),  
    path("subscriptions/", views.subscriptions_view, name="subscriptions"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("subscriptions/delete/<int:pk>/", views.delete_subscription, name="delete_subscription"),
    path("messages/", views.messages_view, name="messages"),
    path("messages/delete/<int:pk>/", views.delete_message, name="delete_message"),
    path("dashboard/projects/", views.dashboard_projects_view, name="dashboard_projects_view"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("messages/<int:pk>/", views.message_detail, name="message_detail"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
=======
    path("about/", views.About, name="About"),
    path("projects/", views.Projects, name="Projects"),
    path("contact/", views.contact, name="contact"),

    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard
    path("dashboard/", views.dashboard_home, name="dashboard_home"),
    path("dashboard/projects/", views.dashboard_projects_view, name="dashboard_projects_view"),
    path("dashboard/add/", views.add_project, name="add_project"),
    path("dashboard/edit/<int:pk>/", views.edit_project, name="edit_project"),
    path("dashboard/delete/<int:pk>/", views.delete_project, name="delete_project"),

    # Contact messages
    path("messages/", views.messages_view, name="messages"),
    path("messages/<int:pk>/", views.message_detail, name="message_detail"),
    path("messages/delete/<int:pk>/", views.delete_message, name="delete_message"),

    # Subscriptions
    path("subscriptions/", views.subscriptions_view, name="subscriptions"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("subscriptions/delete/<int:pk>/", views.delete_subscription, name="delete_subscription"),
    path("unsubscribe/<str:email>/", views.unsubscribe, name="unsubscribe"),

    # Testimonials
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
    path("testimonials/", views.testimonials_view, name="testimonials"),
    path("reviews/", views.all_testimonials, name="all_testimonials"),
    path("projects/add-testimonial/", views.add_testimonial, name="add_testimonial"),
    path("dashboard/testimonial/<int:pk>/approve/", views.approve_testimonial, name="approve_testimonial"),
    path("dashboard/testimonial/<int:pk>/delete/", views.delete_testimonial, name="delete_testimonial"),

    # Testimonial API
    path("projects/load-more/", views.load_more_testimonials, name="load_more_testimonials"),
    path("testimonials_api/", views.testimonials_api, name="testimonials_api"),

    # Project details
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),

    # Portfolio PDF
    path("portfolio/download/", views.generate_portfolio_pdf, name="generate_portfolio_pdf"),
<<<<<<< HEAD
    path("unsubscribe/<str:token>/", views.unsubscribe, name="unsubscribe"),
=======
>>>>>>> 21141a841a24d451fbb4034ee68ab02cee9b3dd9
]
