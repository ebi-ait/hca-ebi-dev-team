class NxnDatabase:
   def __init__(self, data: list(list)):
      self.header = data[0]
      self.__key_to_index = self.__populate_key_to_index_map(self.header)
      self.data = data[1:]

   def __populate_key_to_index_map__(header: list):
      return {k: v for v, k in enumerate(header)}

   def get_value(self, data_row: list, key: str):
      return data_row[self.__key_to_index[key]]

   def get_values(self, key: str) -> set:
      return set(self.get_value(data_row, str) for data_row in self.data if self.get_value(data_row, str))
