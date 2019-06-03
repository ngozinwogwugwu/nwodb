#ifndef ROW_H_
#define ROW_H_

#define COLUMN_USERNAME_SIZE 32
#define COLUMN_EMAIL_SIZE 255
// #define size_of_attribute(Struct, Attribute) sizeof(((Struct*)0)->Attribute);

struct Row_t {
  uint32_t id;
  char username[COLUMN_USERNAME_SIZE + 1];
  char email[COLUMN_EMAIL_SIZE + 1];
};
typedef struct Row_t Row;

#define ID_SIZE         (4) //size_of_attribute(Row, id)
#define USERNAME_SIZE   (33) //size_of_attribute(Row, username)
#define EMAIL_SIZE      (256) //size_of_attribute(Row, email)
#define ID_OFFSET       (0)
#define USERNAME_OFFSET (ID_OFFSET + ID_SIZE)
#define EMAIL_OFFSET    (USERNAME_OFFSET + USERNAME_SIZE)
#define ROW_SIZE        (ID_SIZE + USERNAME_SIZE + EMAIL_SIZE)

void serialize_row(Row* source, void* destination);
void deserialize_row(void* source, Row* destination);
void print_row(Row* row);

#endif /*ROW_H_*/