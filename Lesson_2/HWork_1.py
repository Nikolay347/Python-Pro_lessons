# Створення класу з базовими властивостями типу dict.

class HashTable:
  """
  Клас реалізує хеш-таблицю з реалізацією:
  1. Додавання нових пар ключ:значення;
  2. Вставки пари у правильне місце через хешування і probing;
  3. Отримання значення за ключем;
  4. Масштабування при перевищенні порогу завантаженості (resize);
  5. Обробки колізій за допомогою лінійного пробування (linear probing).
  """

  def __init__(self, size=8):
      """
      Ініціалізація хеш-таблиці.
      size — початковий розмір таблиці (кількість слотів).
      """
      self.size = size
      self.count = 0
      self.load_koef = 0.6      #Коефіцієнт заповнюваності таблиці
      self.table = [None] * size

  def _hash(self, key):
      """
      Приватний метод для обчислення хеш-індексу ключа.
      """
      return hash(key) % self.size

  def _probe(self, index, key):
      """
      Приватний метод для вирішення колізій за допомогою лінійного пробування.
      Повертає індекс, де можна вставити або оновити ключ(його значення).
      """
      start_index = index
      while self.table[index] is not None:
          pair = self.table[index]
          if pair[0] == key:
              return index
          index = (index + 1) % self.size
          if index == start_index:
              raise Exception("HashTable is full")
      return index

  def _resize(self):
      """
      Приватний метод для збільшення розміру таблиці у 2 рази,
      коли поріг завантаженості перевищено. Виконує ре-хешування всіх елементів.
      """
      old_table = self.table
      self.size *= 2
      self.count = 0
      self.table = [None] * self.size
      for item in old_table:
          if item is not None:
              key, value = item
              self.insert(key, value)

  def insert(self, key, value):
      """
      Публічний метод для додавання або оновлення пари ключ:значення.
      Також виконує масштабування, якщо load_koef перевищено.
      """
      if self.count / self.size >= self.load_koef:
          self._resize()
      index = self._hash(key)
      index = self._probe(index, key)
      if self.table[index] is None:
          self.count += 1
      self.table[index] = (key, value)

  def get(self, key, default=None):
      """
      Публічний метод для отримання значення за ключем.
      Повертає default, якщо ключ не знайдено.
      """
      index = self._hash(key)
      start_index = index
      while self.table[index] is not None:
          pair = self.table[index]
          if pair[0] == key:
              return pair[1]
          index = (index + 1) % self.size
          if index == start_index:
              break
      return default

  def __str__(self):
      """
      Повертає текстове представлення хеш-таблиці.
      """
      pairs = [f"{k}: {v}" for item in self.table if item is not None for k, v in [item]]
      return "{" + ", ".join(pairs) + "}"


# ========================
# Приклади верифікації
# ========================

fructs = HashTable()  # Початковий розмір 8

# 1. Додавання нової пари ключ:значення
fructs.insert("apple", 10)
fructs.insert("banana", 20)
print("Після додавання apple і banana:", fructs)

# 2. Вставка в правильне місце через обчислення індексу
fructs.insert("orange", 30)
print("Після додавання orange:", fructs)

# 3. Отримання значення за ключем
print("Значення за ключем 'apple':", fructs.get("apple"))

# 4. Маштабування хеш-таблиці при перевищенні load_koef
fructs.insert("grape", 40)
fructs.insert("melon", 50)
fructs.insert("peach", 60)
print("Після додавання grape, melon, peach:", fructs)
print("Поточний розмір таблиці:", fructs.size)

