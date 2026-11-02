from django.contrib.auth import views as auth_views
from django.urls import path

from .views import bench, desk, inventory, records

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", records.home, name="home"),
    path("store/", records.switch_store, name="switch_store"),
    path("access/", records.access, name="access"),
    path("dashboard/", records.dashboard, name="dashboard"),
    # Front Desk: appointments, check-in, approval, pickup (DFD 1.0, 2.0, 5.0, 6.0)
    path("checkin/", desk.checkin, name="checkin"),
    path("appointments/new/", desk.appointment_edit, name="appointment_new"),
    path("appointments/<int:pk>/", desk.appointment_edit, name="appointment_edit"),
    path("appointments/<int:pk>/cancel/", desk.appointment_cancel, name="appointment_cancel"),
    path("jobs/", desk.jobs, name="jobs"),
    path("jobs/<int:pk>/", desk.job_detail, name="job_detail"),
    path("jobs/<int:pk>/ticket/", desk.job_ticket, name="job_ticket"),
    path("jobs/<int:pk>/notify/", desk.job_notify, name="job_notify"),
    # Technician: diagnosis, quote, repair (DFD 3.0, 4.0)
    path("bench/", bench.bench, name="bench"),
    path("bench/<int:pk>/", bench.bench, name="bench_job"),
    # Manager: inventory and purchase orders (DFD 7.0, 9.0)
    path("inventory/", inventory.inventory, name="inventory"),
    path("inventory/parts/new/", inventory.part_edit, name="part_new"),
    path("inventory/parts/<int:pk>/", inventory.part_edit, name="part_edit"),
    path("inventory/import/", inventory.import_csv, name="inventory_import"),
    path("orders/", inventory.po_list, name="po_list"),
    path("orders/<int:pk>/", inventory.po_detail, name="po_detail"),
    # Records (DFD 9.0, FR14)
    path("staff/", records.staff, name="staff"),
    path("staff/new/", records.staff_edit, name="staff_new"),
    path("staff/<int:pk>/", records.staff_edit, name="staff_edit"),
    path("suppliers/new/", records.supplier_edit, name="supplier_new"),
    path("suppliers/<int:pk>/", records.supplier_edit, name="supplier_edit"),
    path("stores/<int:pk>/", records.store_edit, name="store_edit"),
]
