from auto_everything.database import MongoDB

mongoDB = MongoDB("mongodb://yingshaoxo:yingshaoxo@127.0.0.1:27017/")

object_database_name = "it_has_alternatives_object"
object_collection = mongoDB.get_database(object_database_name).get_collection(object_database_name) #type: ignore
user_collection = mongoDB.get_database(object_database_name).get_collection("user") #type: ignore

print(object_collection)
print(user_collection)

mongoDB.backup_mongodb("./data_backup", use_time_as_sub_folder_name=False)
