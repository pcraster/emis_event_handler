import smtplib


def send_mail(
        smtp_server,
        smtp_port,
        smtp_sender,
        recipients,
        subject,
        message):
    headers = (
        "From: {}\r\n"
        "To: \r\n"
        "Date: \r\n"
        "Subject: {}\r\n\r\n".format(smtp_sender, subject))
    smtp_server = smtplib.SMTP()
    smtp_server.connect(smtp_server, smtp_port)
    smtp_server.sendmail(smtp_sender, recipients, headers + str(message))
    smtp_server.close()


# import os
# import requests
# import lue
# 
# 
# def scan_for_regular_files(
#         directory_pathname):
# 
#     for (_, _, filenames) in os.walk(directory_pathname):
#         pathnames = [os.path.join(directory_pathname, n) for n in filenames]
#         break
# 
#     return pathnames
# 
# 
# class Property(object):
# 
#     def __init__(self,
#             dataset_pathname,
#             property_pathname):
#         self.dataset_pathname = dataset_pathname
#         self.property_pathname = property_pathname
# 
#     def __repr__(self):
#             return "Property({}, {})".format(
#                 self.dataset_pathname, self.property_pathname)
# 
#     def __eq__(self,
#             other):
#         return \
#             self.dataset_pathname == other.dataset_pathname and \
#             self.property_pathname == other.property_pathname
# 
# 
# def scan_phenomena_for_properties(
#         phenomena):
# 
#     property_pathnames = []
# 
#     for phenomenon_name in phenomena.names:
#         phenomenon = phenomena[phenomenon_name]
#         property_sets = phenomenon.property_sets
# 
#         for property_set_name in property_sets.names:
#             property_set = property_sets[property_set_name]
#             properties_ = property_set.properties
# 
#             for property_name in properties_.names:
#                 property = properties_[property_name]
#                 property_pathnames.append(property.id.pathname)
# 
#     return property_pathnames
# 
# 
# def scan_universes_for_properties(
#         universes):
# 
#     property_pathnames = []
# 
#     for universe_name in universes.names:
#         universe = universes[universe_name]
#         phenomena = universe.phenomena
#         property_pathnames += scan_phenomena_for_properties(phenomena)
# 
#     return property_pathnames
# 
# 
# def scan_for_properties(
#         pathname):
# 
#     properties = []
# 
#     if os.path.isdir(pathname):
#         pathnames = scan_for_regular_files(pathname)
# 
#         for pathname in pathnames:
#             properties += scan_for_properties(pathname)
#     else:
# 
#         # See if we can open the file as a LUE dataset. If not, issue a
#         # warning. If so, obtain the internal paths of properties.
#         try:
# 
#             dataset = lue.open_dataset(pathname, lue.access_flag.ro)
#             properties += [Property(pathname, property_pathname) for
#                 property_pathname in scan_phenomena_for_properties(
#                     dataset.phenomena)]
#             properties += [Property(pathname, property_pathname) for
#                 property_pathname in scan_universes_for_properties(
#                     dataset.universes)]
# 
#         except RuntimeError:
#             pass
#             print("Skipping non-LUE file {}".format(pathname))
# 
#     return properties
# 
# 
# def property_equals(
#         available_property,
#         property):
#     return \
#         available_property["pathname"] == property.dataset_pathname and \
#         available_property["name"] == property.property_pathname
# 
# 
# def property_already_available(
#         available_properties,
#         property):
# 
#     return any([property_equals(available_property, property) for
#         available_property in available_properties])
# 
# 
# def add_property(
#         uri,
#         property):
# 
#     payload = {
#         "name": property.property_pathname,
#         "pathname": property.dataset_pathname
#     }
# 
#     response = requests.post(uri, json={"property": payload})
# 
#     if response.status_code != 201:
#         raise RuntimeError(response.json()["message"])
# 
# 
# def rewrite_pathnames(
#         properties,
#         rewrite_path):
#     """
#     Rewrite pathnames *in-place*
#     """
# 
#     if rewrite_path is not None and rewrite_path:
#         assert len(rewrite_path) == 2, rewrite_path
# 
#         for property in properties:
#             if property.dataset_pathname.startswith(rewrite_path[0]):
#                 property.dataset_pathname = property.dataset_pathname.replace(
#                     rewrite_path[0], rewrite_path[1])
# 
#     return properties
# 
# 
# def scan(
#         uri,
#         pathnames,
#         rewrite_path=None):
# 
#     properties = []
# 
#     for pathname in pathnames:
#         properties += scan_for_properties(pathname)
# 
#     properties = rewrite_pathnames(properties, rewrite_path)
#     response = requests.get(uri)
# 
#     if response.status_code != 200:
#         raise RuntimeError("cannot get collection of properties")
# 
#     available_properties = response.json()["properties"]
# 
#     for property in properties:
#         if not property_already_available(available_properties, property):
#             add_property(uri, property)
