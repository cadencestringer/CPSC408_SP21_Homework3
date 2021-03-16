CREATE TABLE StudentDB
(
    StudentId         INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName         TEXT,
    LastName          TEXT,
    GPA               REAL,
    Major             TEXT,
    FacultyAdvisor    TEXT,
    Address           TEXT,
    City              TEXT,
    State             TEXT,
    ZipCode           TEXT,
    MobilePhoneNumber TEXT,
    isDeleted         INTEGER
);

