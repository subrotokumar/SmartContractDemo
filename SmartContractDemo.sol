// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SmartContractDemo {
    struct Person {
        string name;
        string dateOfBirth;
    }

    Person[] public idCard;

    function numberOfEntries() public view returns (uint256) {
        return idCard.length;
    }

    function store(string memory _name, string memory _birthday) public {
        idCard.push(Person(_name, _birthday));
    }

    function changeData(
        uint256 index,
        string memory _name,
        string memory _birthday
    ) public {
        require(index <= numberOfEntries(), "Given index not present");
        idCard[index] = Person(_name, _birthday);
    }

    function retrieve(uint256 index)
        public
        view
        returns (string memory, string memory)
    {
        require(index <= numberOfEntries(), "Given index not present");
        return (idCard[index].name, idCard[index].dateOfBirth);
    }
}