/* 
These are network related resources.

We will create a public subnet with an internet gateway
so our task can reach the internet both ways.

Based on AWS example here https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/services/ECS/FargateLaunchType/clusters/public-vpc.yml
Want to understand routes? https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html

Short Description
---
1. A VPC to group everything
2. An internet gateway (Literally a door -gateway- to access internet)
3. A Public Subnet to reach the task from internet
    2.1. An Internet gateway is required for internet access
    2.2. Route Table rule that delegates all task requests (0.0.0.0/0) to the igw (Like if it were a router and a pc)

Long Description
---
0. Asociate InternetGateway to VPC
  VPC --GatewayAttachement--> InternetGateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
  GatewayAttachement:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref 'VPC'
      InternetGatewayId: !Ref 'InternetGateway'

1. Add Route Table to configure outbound traffic to InternetGateway
RouteTable 
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref 'VPC'

  - Route to internet.
    Send all outbound traffic via the gateway.
    PublicRoute:
      Type: AWS::EC2::Route
      DependsOn: GatewayAttachement
      Properties:
        RouteTableId: !Ref 'PublicRouteTable'
        DestinationCidrBlock: '0.0.0.0/0'
        GatewayId: !Ref 'InternetGateway'

  - Link Route Table with Subnet
  PublicSubnetOneRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnetOne
      RouteTableId: !Ref PublicRouteTable
*/

# The VPC
resource "aws_vpc" "main" {
  # Base network mask for all potential subnets
  # They will all look like 10.0.X.0/24, where X is 1,2..n
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "ambro-vpc"
  }
}

# Add an internet door/gateway to the VPC
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Asociate route table with subnet
resource "aws_route_table_association" "subnet_route_table" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.routing_table_public.id
}

# Add a subnet inside the vpc
resource "aws_subnet" "public" {
  vpc_id = aws_vpc.main.id
  # Note the base CIDR was 10.0.0.0/16
  cidr_block = "10.0.1.0/24"
  
  # Instances launched in this subnet should get assigned an IP on launch
  map_public_ip_on_launch = true
} 

# Add a route table to tell the vpc to use the internet gateway for networking
resource "aws_route_table" "routing_table_public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}