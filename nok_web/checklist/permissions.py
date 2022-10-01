from rest_framework import permissions


# Касстомный класс, позволяющий чтобы запись мог просматривать каждый, а удалять только Администратор
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permissioons(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)



# Запись менять может только пользователь который её создал и Аминистратор, просматривать может любой
class IsOwnerAndAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение на уровне объекта, позволяющее редактировать его только владельцам объекта.
    Предполагается, что экземпляр модели имеет атрибут `user`.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user or bool(request.user.is_staff)