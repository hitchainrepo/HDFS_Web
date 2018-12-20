from django.db import models

class Repo(models.Model):
    username = models.CharField(max_length=255)
    reponame = models.CharField(max_length=255)
    ipfs_hash = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = "repo"


class Authority(models.Model):
    username = models.CharField(max_length=255)
    repo_id = models.IntegerField()
    user_type = models.CharField(max_length=255, default="owner")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = "authority"

class StorageReport(models.Model):
    node_id = models.CharField(max_length=255)
    repo_size = models.CharField(max_length=255)
    storage_size = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.node_id
    class Meta:
        db_table = "storage_report"

class StorageCheck(models.Model):
    node_id = models.CharField(max_length=255)
    ping_result = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.node_id
    class Meta:
        db_table = "storage_check"

class TemporaryPubKey(models.Model):
    node_id = models.CharField(max_length=255)
    public_key = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.node_id
    class Meta:
        db_table = "temporary_public_key"

class Clients(models.Model):
    node_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.node_id
    class Meta:
        db_table = "clients"

class Servers(models.Model):
    node_id = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)

    def __str__(self):
        return self.node_id
    class Meta:
        db_table = "servers"