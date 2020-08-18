#include <string>
#include <iostream>
#include <string>
#include <iomanip>

using namespace std;

struct Salary {
private:
    int _month;
    int _hoursWorked = 0;
    float _perHourRate = 0;
    int _taxRate = 0;

public:
    Salary(){};
    Salary(int month, int hoursWorked, float perHourRate, int taxRate)
    {
        this->_month = month;
        this->_hoursWorked = hoursWorked;
        this->_perHourRate = perHourRate;
        this->_taxRate = taxRate;
    }
    void setMonth(int month)
    {
        if (month <= 12) {
            this->_month = month;
        }
        else {
            this->_month = 12;
        }
    }
    void setHoursWorked(int hoursWorked)
    {
        this->_hoursWorked = hoursWorked;
    }
    void setPerHourRate(int perHourRate)
    {
        this->_perHourRate = perHourRate;
    }
    void setTaxRate(int taxRate)
    {
        this->_taxRate = taxRate;
    }
    int const getMonth()
    {
        return this->_month;
    }
    float const getMonthlySalary()
    {
        return this->_hoursWorked * this->_perHourRate * this->getAward();
    }
    float getAward()
    {
        float award;
        if (_hoursWorked > 25) {
            award = this->_perHourRate * 1.01;
        }
        else if (_hoursWorked > 35) {
            award = this->_perHourRate * 1.01;
        }
        else if (_hoursWorked > 40) {
            award = this->_perHourRate * 1.01;
        }
        return award;
    }
    friend ostream& operator<<(ostream& os, Salary& salary);
    friend ostream& operator<<(ostream& os, Salary salaries[]);
};

ostream& operator<<(ostream& os, Salary& salary)
{
    os << "  Month: " << salary._month << " Salary: " << setw(4) << salary.getMonthlySalary() << endl;
    return os;
}

ostream& operator<<(ostream& os, Salary salaries[])
{
    for (int i = 0; i < 13; i++) {
        Salary salary = salaries[i];
        os << "Month: " << salary._month << " Salary: " << setw(4) << salary.getMonthlySalary() << endl;
    }
    return os;
}

class Employee {
private:
    string _name;
    string _idNumber;
    string _department;
    string _position;
    Salary _salaries[13];

public:
    Employee(string name, string idNumber, string department, string position)
    {
        this->_name = name;
        this->_idNumber = idNumber;
        this->_department = department;
        this->_position = position;
        setSalaries();
    }
    Employee(string name, string idNumber)
    {
        this->_name = name;
        this->_idNumber = idNumber;
        this->_department = " ";
        this->_position = " ";
        setSalaries();
    }
    Employee()
    {
        this->_name = "";
        this->_idNumber = "";
        this->_department = "";
        this->_position = "";
        setSalaries();
    }
    string const getName()
    {
        return this->_name;
    }
    string const getId()
    {
        return this->_idNumber;
    }
    string const getDepartment()
    {
        return this->_department;
    }
    string const getPosition()
    {
        return this->_position;
    }
    Salary getSalary(int month)
    {
        return this->_salaries[month - 1];
    }
    Salary* getSalaries()
    {
        return this->_salaries;
    }
    void init(string name, string idNumber, string department, string position)
    {
        this->_name = name;
        this->_idNumber = idNumber;
        this->_department = department;
        this->_position = position;
        setSalaries();
    }
    void setName(string name)
    {
        this->_name = name;
    }
    void setId(string idNumber)
    {
        this->_idNumber = idNumber;
    }
    void setDepartment(string department)
    {
        this->_department = department;
    }
    void setPosition(string position)
    {
        this->_position = position;
    }
    void setSalary(int month, int hoursWorked, float perHourRate, int taxRate)
    {
        this->_salaries[month - 1] = Salary(month, hoursWorked, perHourRate, taxRate);
    }
    void setSalaries()
    {
        for (int i = 0; i < 13; i++) {
            this->_salaries[i].setMonth(i);
        }
    }
    friend ostream& operator<<(ostream& os, const Employee& employee);
    friend ostream& operator<<(ostream& os, Employee* employee);
};

ostream& operator<<(ostream& os, const Employee& employee)
{
    os << employee._idNumber << setw(14) << employee._name << setw(14) << employee._position << endl;
    return os;
}

ostream& operator<<(ostream& os, Employee* employee)
{
    os << employee->getId() << setw(14) << employee->getName() << setw(14) << employee->getPosition();
    return os;
}

Employee* fillEmployeeList()
{
    Employee* employeeList = new Employee[100];
    employeeList[0].init("Jenny Jacobs", "JJ8990", "Accounting", "President");
    employeeList[0].setSalary(1, 45, 3.5, 7);
    employeeList[1].init("Myron Smith", "MS7571", "IT", "Programmer");
    employeeList[1].setSalary(1, 35, 4.5, 7);
    employeeList[2].init("Chris Raines", "CR6873", "Manufacturing", "Engineer");
    employeeList[2].setSalary(1, 25, 3.5, 7);
    return employeeList;
}

Employee* addNewEmployee(Employee* employeeList, int employeeNumber)
{
    string employeeName;
    string employeeId;
    string employeeDepartment;
    string employeePosition;
    cout << "Enter an employee name:" << endl;
    cin >> employeeName;
    cout << "Enter an employee id:" << endl;
    cin >> employeeId;
    cout << "Enter an employee department:" << endl;
    cin >> employeeDepartment;
    cout << "Enter an employee position:" << endl;
    cin >> employeePosition;
    employeeList[employeeNumber].init(employeeName, employeeId, employeeDepartment, employeePosition);
    return employeeList;
}

void displayEmployeeList(Employee* employeeList, int employeeNumber)
{
    for (int i = 0; i < employeeNumber; i++) {
        cout << "--------------------------------" << endl;
        cout << employeeList[i];
    }
}
void displayDetailedEmployeeList(Employee* employeeList, int employeeNumber)
{
    for (int i = 0; i < employeeNumber; i++) {
        cout << "--------------------------------" << endl;
        cout << employeeList[i];
        cout << employeeList[i].getSalaries();
    }
}
void displayMonthSalaryReport(Employee* employeeList, int employeeNumber)
{
    int month;
    cout << "Enter the month:";
    cin >> month;
    for (int i = 0; i < employeeNumber; i++) {
        cout << "--------------------------------" << endl;
        Salary salary = employeeList[i].getSalary(month);
        cout << employeeList[i].getName() << setw(10) << salary << endl;
    }
}

void welcomeMessage()
{
    cout << "--------------------------------" << endl;
    cout << "Welcome! Enter a number:" << endl;
    cout << "1 - display all employees" << endl;
    cout << "2 - display a detailed list of the all employees and their salaries" << endl;
    cout << "3 - display the month salary report" << endl;
    cout << "4 - add a new employee" << endl;
    cout << "5 - exit" << endl;
    cout << "--------------------------------" << endl;
}
int main()
{
    Employee* employeeList = fillEmployeeList();
    fillEmployeeList();
    int employeeNumber = 3;
    int choice;
    do {
        welcomeMessage();
        cin >> choice;

        switch (choice) {
        case 1:
            displayEmployeeList(employeeList, employeeNumber);
            break;
        case 2:
            displayDetailedEmployeeList(employeeList, employeeNumber);
            break;
        case 3:
            displayMonthSalaryReport(employeeList, employeeNumber);
            break;
        case 4:
            employeeList = addNewEmployee(employeeList, employeeNumber);
            employeeNumber++;
            break;
        case 5:
            return 0;
        }
    } while (choice != 5);

    return 0;
}