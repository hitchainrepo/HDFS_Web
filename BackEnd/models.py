from django.db import models

class Repo(models.Model):
    username = models.CharField(max_length=255)
    reponame = models.CharField(max_length=255)
    ipfs_hash = models.CharField(max_length=255)
    create_time = models.DateTimeField()

    def __str__(self):
        return self.username
    class Meta:
        db_table = "repo"


class Authority(models.Model):
    username = models.CharField(max_length=255)
    repo_id = models.IntegerField()
    user_type = models.CharField(max_length=255, default="owner")
    create_time = models.DateTimeField()

    def __str__(self):
        return self.username
    class Meta:
        db_table = "authority"

class StorageReport(models.Model):
    node_id = models.CharField(max_length=255)
    repo_size = models.BigIntegerField()
    storage_size = models.BigIntegerField()
    create_time = models.DateTimeField()

    def __str__(self):
        return self.node_id
    class Meta:
        db_table = "storage_report"

class StorageCheck(models.Model):
    node_id = models.CharField(max_length=255)
    ping_result = models.BooleanField()
    create_time = models.DateTimeField()

    def __str__(self):
        return self.node_id
    class Meta:
        db_table = "storage_check"