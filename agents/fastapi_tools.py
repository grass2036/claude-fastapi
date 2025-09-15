"""
FastAPI后端开发专用工具集
为FastAPI后端开发Agent提供专门的工具
"""

import os
import re
from typing import Type, Any, Dict, List, Optional
from pathlib import Path
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from .claude_integration import claude_integration


class APIGenerationInput(BaseModel):
    """API生成输入模型"""
    resource_name: str = Field(..., description="资源名称，如 'users', 'products'")
    model_name: str = Field(..., description="模型名称，如 'User', 'Product'")
    include_crud: bool = Field(default=True, description="是否包含CRUD操作")
    include_auth: bool = Field(default=True, description="是否包含权限验证")
    custom_endpoints: List[str] = Field(default=[], description="自定义端点列表")


class APIGenerationTool(BaseTool):
    """FastAPI路由生成工具"""
    name: str = "fastapi_api_generator"
    description: str = "生成完整的FastAPI路由文件，包含CRUD操作和权限验证"
    args_schema: Type[BaseModel] = APIGenerationInput
    
    def _run(
        self, 
        resource_name: str, 
        model_name: str,
        include_crud: bool = True,
        include_auth: bool = True,
        custom_endpoints: List[str] = []
    ) -> str:
        """生成FastAPI路由文件"""
        try:
            # 生成路由代码模板
            router_code = self._generate_router_template(
                resource_name, model_name, include_crud, include_auth, custom_endpoints
            )
            
            # 保存到文件
            file_path = f"/Users/chiyingjie/code/git/claude-fastapi/backend/api/v1/{resource_name}.py"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(router_code)
            
            return f"✅ 成功生成FastAPI路由文件: {file_path}\n\n预览:\n{router_code[:500]}..."
            
        except Exception as e:
            return f"❌ API生成失败: {str(e)}"
    
    def _generate_router_template(
        self, 
        resource_name: str, 
        model_name: str,
        include_crud: bool,
        include_auth: bool,
        custom_endpoints: List[str]
    ) -> str:
        """生成路由代码模板"""
        
        # 基础导入和路由设置
        template = f'''from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from ...api.deps import get_current_active_user, get_current_superuser, get_current_user
from ...crud.{resource_name.rstrip('s')} import {resource_name.rstrip('s')}_crud
from ...db.base import get_db'''

        if include_auth:
            template += f'''
from ...middleware.permission import (
    PermissionAction,
    ResourceType,
    require_permission,
    require_read_permission,
    require_write_permission,
)'''

        template += f'''
from ...models.{resource_name.rstrip('s')} import {model_name}
from ...schemas.{resource_name.rstrip('s')} import {model_name}Create, {model_name}Response, {model_name}Update

router = APIRouter()

'''

        # 如果包含CRUD操作，生成标准CRUD端点
        if include_crud:
            template += self._generate_crud_endpoints(resource_name, model_name, include_auth)
        
        # 添加自定义端点
        for endpoint in custom_endpoints:
            template += self._generate_custom_endpoint(endpoint, resource_name, model_name, include_auth)
        
        return template
    
    def _generate_crud_endpoints(self, resource_name: str, model_name: str, include_auth: bool) -> str:
        """生成标准CRUD端点"""
        singular = resource_name.rstrip('s')
        auth_decorator = ""
        auth_params = ""
        
        if include_auth:
            resource_type = f"ResourceType.{singular.upper()}"
            auth_params = '''
    request: Request,
    current_user: {model_name} = Depends(get_current_user),'''

        return f'''
# 创建{model_name}
@router.post(
    "/",
    response_model={model_name}Response,
    summary="创建{model_name}",
    description="创建新的{model_name}记录",
    status_code=status.HTTP_201_CREATED
)
{"@require_write_permission(" + resource_type + ")" if include_auth else ""}
async def create_{singular}(
    {singular}_data: {model_name}Create,{auth_params}
    db: Session = Depends(get_db)
):
    """创建{model_name}"""
    new_{singular} = {singular}_crud.create_{singular}(db, {singular}_data)
    return new_{singular}


# 获取{model_name}列表
@router.get(
    "/",
    response_model=List[{model_name}Response],
    summary="获取{model_name}列表",
    description="获取{model_name}列表，支持分页和筛选"
)
{"@require_read_permission(" + resource_type + ")" if include_auth else ""}
async def get_{resource_name}(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),{auth_params}
    db: Session = Depends(get_db)
):
    """获取{model_name}列表"""
    {resource_name} = {singular}_crud.get_{resource_name}(db, skip=skip, limit=limit)
    return {resource_name}


# 获取单个{model_name}
@router.get(
    "/{{{singular}_id}}",
    response_model={model_name}Response,
    summary="获取{model_name}详情",
    description="根据ID获取{model_name}详细信息"
)
{"@require_permission(" + resource_type + ", PermissionAction.READ, resource_id_param=\"" + singular + "_id\")" if include_auth else ""}
async def get_{singular}(
    {singular}_id: int,{auth_params}
    db: Session = Depends(get_db)
):
    """获取单个{model_name}"""
    {singular} = {singular}_crud.get_{singular}(db, {singular}_id)
    if not {singular}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{model_name}不存在"
        )
    return {singular}


# 更新{model_name}
@router.put(
    "/{{{singular}_id}}",
    response_model={model_name}Response,
    summary="更新{model_name}",
    description="根据ID更新{model_name}信息"
)
{"@require_permission(" + resource_type + ", PermissionAction.UPDATE, resource_id_param=\"" + singular + "_id\")" if include_auth else ""}
async def update_{singular}(
    {singular}_id: int,
    {singular}_update: {model_name}Update,{auth_params}
    db: Session = Depends(get_db)
):
    """更新{model_name}"""
    updated_{singular} = {singular}_crud.update_{singular}(db, {singular}_id, {singular}_update)
    if not updated_{singular}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{model_name}不存在"
        )
    return updated_{singular}


# 删除{model_name}
@router.delete(
    "/{{{singular}_id}}",
    summary="删除{model_name}",
    description="根据ID删除{model_name}"
)
{"@require_permission(" + resource_type + ", PermissionAction.DELETE, resource_id_param=\"" + singular + "_id\")" if include_auth else ""}
async def delete_{singular}(
    {singular}_id: int,{auth_params}
    db: Session = Depends(get_db)
):
    """删除{model_name}"""
    success = {singular}_crud.delete_{singular}(db, {singular}_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{model_name}不存在"
        )
    return {{"message": "{model_name}已删除", "{singular}_id": {singular}_id}}
'''
    
    def _generate_custom_endpoint(self, endpoint_name: str, resource_name: str, model_name: str, include_auth: bool) -> str:
        """生成自定义端点"""
        return f'''

# 自定义端点: {endpoint_name}
@router.post(
    "/{endpoint_name}",
    summary="{endpoint_name}",
    description="自定义{model_name}操作: {endpoint_name}"
)
async def {endpoint_name.replace('-', '_')}():
    """自定义操作: {endpoint_name}"""
    # TODO: 实现{endpoint_name}逻辑
    return {{"message": "{endpoint_name}操作完成"}}
'''


class ModelGenerationInput(BaseModel):
    """数据模型生成输入"""
    model_name: str = Field(..., description="模型名称，如 'Product'")
    table_name: str = Field(..., description="表名，如 'products'")
    fields: Dict[str, str] = Field(..., description="字段定义，格式: {字段名: 字段类型}")
    include_timestamps: bool = Field(default=True, description="是否包含时间戳字段")
    include_relationships: List[str] = Field(default=[], description="关系字段列表")


class ModelGenerationTool(BaseTool):
    """SQLAlchemy模型生成工具"""
    name: str = "fastapi_model_generator"
    description: str = "生成SQLAlchemy数据模型文件"
    args_schema: Type[BaseModel] = ModelGenerationInput
    
    def _run(
        self,
        model_name: str,
        table_name: str,
        fields: Dict[str, str],
        include_timestamps: bool = True,
        include_relationships: List[str] = []
    ) -> str:
        """生成SQLAlchemy模型"""
        try:
            model_code = self._generate_model_template(
                model_name, table_name, fields, include_timestamps, include_relationships
            )
            
            # 保存到文件
            file_path = f"/Users/chiyingjie/code/git/claude-fastapi/backend/models/{table_name.rstrip('s')}.py"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(model_code)
            
            return f"✅ 成功生成SQLAlchemy模型: {file_path}\n\n预览:\n{model_code[:500]}..."
            
        except Exception as e:
            return f"❌ 模型生成失败: {str(e)}"
    
    def _generate_model_template(
        self,
        model_name: str,
        table_name: str,
        fields: Dict[str, str],
        include_timestamps: bool,
        include_relationships: List[str]
    ) -> str:
        """生成模型代码模板"""
        
        imports = ["from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Float, ForeignKey"]
        if include_relationships:
            imports.append("from sqlalchemy.orm import relationship")
        if include_timestamps:
            imports.append("from sqlalchemy.sql import func")
        
        template = f'''{"".join(import_line + chr(10) for import_line in imports)}

# 绝对导入，避免相对导入问题
try:
    from backend.db.base import Base
except ImportError:
    from db.base import Base


class {model_name}(Base):
    """{model_name}模型"""
    
    __tablename__ = "{table_name}"
    
    id = Column(Integer, primary_key=True, index=True, comment="{model_name}ID")
'''
        
        # 添加字段定义
        for field_name, field_type in fields.items():
            template += f'    {field_name} = Column({self._map_field_type(field_type)}, comment="{field_name}")\n'
        
        # 添加时间戳字段
        if include_timestamps:
            template += '''
    # 时间字段
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )
'''
        
        # 添加关系字段
        for relationship in include_relationships:
            template += f'    {relationship} = relationship("{relationship.title()}", back_populates="{table_name}")\n'
        
        # 添加方法
        template += f'''
    def __repr__(self):
        return f"<{model_name}(id={{self.id}})>"
'''
        
        return template
    
    def _map_field_type(self, field_type: str) -> str:
        """映射字段类型到SQLAlchemy类型"""
        type_mapping = {
            'string': 'String(255)',
            'text': 'Text',
            'int': 'Integer',
            'integer': 'Integer',
            'float': 'Float',
            'bool': 'Boolean',
            'boolean': 'Boolean',
            'datetime': 'DateTime'
        }
        return type_mapping.get(field_type.lower(), 'String(255)')


class CRUDGenerationInput(BaseModel):
    """CRUD生成输入"""
    model_name: str = Field(..., description="模型名称")
    include_advanced_queries: bool = Field(default=True, description="是否包含高级查询方法")


class CRUDGenerationTool(BaseTool):
    """CRUD操作生成工具"""
    name: str = "fastapi_crud_generator"
    description: str = "生成FastAPI CRUD操作文件"
    args_schema: Type[BaseModel] = CRUDGenerationInput
    
    def _run(self, model_name: str, include_advanced_queries: bool = True) -> str:
        """生成CRUD操作文件"""
        try:
            crud_code = self._generate_crud_template(model_name, include_advanced_queries)
            
            # 保存到文件
            singular_name = model_name.lower()
            file_path = f"/Users/chiyingjie/code/git/claude-fastapi/backend/crud/{singular_name}.py"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(crud_code)
            
            return f"✅ 成功生成CRUD文件: {file_path}\n\n预览:\n{crud_code[:500]}..."
            
        except Exception as e:
            return f"❌ CRUD生成失败: {str(e)}"
    
    def _generate_crud_template(self, model_name: str, include_advanced_queries: bool) -> str:
        """生成CRUD代码模板"""
        singular_name = model_name.lower()
        plural_name = singular_name + 's'
        
        template = f'''from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from ..models.{singular_name} import {model_name}
from ..schemas.{singular_name} import {model_name}Create, {model_name}Update


class {model_name}CRUD:
    """{model_name} CRUD操作类"""
    
    def create_{singular_name}(self, db: Session, {singular_name}_data: {model_name}Create) -> {model_name}:
        """创建{model_name}"""
        db_{singular_name} = {model_name}(**{singular_name}_data.dict())
        db.add(db_{singular_name})
        db.commit()
        db.refresh(db_{singular_name})
        return db_{singular_name}
    
    def get_{singular_name}(self, db: Session, {singular_name}_id: int) -> Optional[{model_name}]:
        """根据ID获取{model_name}"""
        return db.query({model_name}).filter({model_name}.id == {singular_name}_id).first()
    
    def get_{plural_name}(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 20,
        order_by: str = "id",
        desc: bool = False
    ) -> List[{model_name}]:
        """获取{model_name}列表"""
        query = db.query({model_name})
        
        # 排序
        order_column = getattr({model_name}, order_by, {model_name}.id)
        if desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
        
        return query.offset(skip).limit(limit).all()
    
    def update_{singular_name}(
        self, 
        db: Session, 
        {singular_name}_id: int, 
        {singular_name}_update: {model_name}Update
    ) -> Optional[{model_name}]:
        """更新{model_name}"""
        db_{singular_name} = db.query({model_name}).filter({model_name}.id == {singular_name}_id).first()
        if not db_{singular_name}:
            return None
        
        update_data = {singular_name}_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_{singular_name}, field, value)
        
        db.commit()
        db.refresh(db_{singular_name})
        return db_{singular_name}
    
    def delete_{singular_name}(self, db: Session, {singular_name}_id: int) -> bool:
        """删除{model_name}"""
        db_{singular_name} = db.query({model_name}).filter({model_name}.id == {singular_name}_id).first()
        if not db_{singular_name}:
            return False
        
        db.delete(db_{singular_name})
        db.commit()
        return True
    
    def get_{plural_name}_count(self, db: Session) -> int:
        """获取{model_name}总数"""
        return db.query({model_name}).count()
'''
        
        if include_advanced_queries:
            template += f'''
    def search_{plural_name}(
        self, 
        db: Session, 
        search_term: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[{model_name}]:
        """搜索{model_name}"""
        # TODO: 根据实际字段实现搜索逻辑
        query = db.query({model_name})
        # 示例：如果有name字段
        # query = query.filter({model_name}.name.ilike(f"%{{search_term}}%"))
        return query.offset(skip).limit(limit).all()
    
    def get_active_{plural_name}(self, db: Session) -> List[{model_name}]:
        """获取活跃的{model_name}"""
        # TODO: 根据实际业务逻辑实现
        return db.query({model_name}).all()
'''
        
        template += f'''

# 创建全局CRUD实例
{singular_name}_crud = {model_name}CRUD()
'''
        
        return template


class SchemaGenerationInput(BaseModel):
    """Schema生成输入"""
    model_name: str = Field(..., description="模型名称")
    fields: Dict[str, str] = Field(..., description="字段定义")
    include_base_schemas: bool = Field(default=True, description="是否包含基础Schema类")


class SchemaGenerationTool(BaseTool):
    """Pydantic Schema生成工具"""
    name: str = "fastapi_schema_generator"
    description: str = "生成Pydantic验证Schema文件"
    args_schema: Type[BaseModel] = SchemaGenerationInput
    
    def _run(
        self,
        model_name: str,
        fields: Dict[str, str],
        include_base_schemas: bool = True
    ) -> str:
        """生成Pydantic Schema"""
        try:
            schema_code = self._generate_schema_template(model_name, fields, include_base_schemas)
            
            # 保存到文件
            singular_name = model_name.lower()
            file_path = f"/Users/chiyingjie/code/git/claude-fastapi/backend/schemas/{singular_name}.py"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(schema_code)
            
            return f"✅ 成功生成Schema文件: {file_path}\n\n预览:\n{schema_code[:500]}..."
            
        except Exception as e:
            return f"❌ Schema生成失败: {str(e)}"
    
    def _generate_schema_template(self, model_name: str, fields: Dict[str, str], include_base_schemas: bool) -> str:
        """生成Schema代码模板"""
        template = f'''from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class {model_name}Base(BaseModel):
    """{model_name}基础Schema"""
'''
        
        # 添加基础字段
        for field_name, field_type in fields.items():
            pydantic_type = self._map_to_pydantic_type(field_type)
            template += f'    {field_name}: {pydantic_type}\n'
        
        template += f'''


class {model_name}Create({model_name}Base):
    """{model_name}创建Schema"""
    pass


class {model_name}Update(BaseModel):
    """{model_name}更新Schema"""
'''
        
        # 更新Schema的字段都是可选的
        for field_name, field_type in fields.items():
            pydantic_type = self._map_to_pydantic_type(field_type)
            if not pydantic_type.startswith('Optional'):
                pydantic_type = f"Optional[{pydantic_type}] = None"
            template += f'    {field_name}: {pydantic_type}\n'
        
        template += f'''


class {model_name}Response({model_name}Base):
    """{model_name}响应Schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class {model_name}Profile({model_name}Response):
    """{model_name}档案Schema"""
    pass
'''
        
        return template
    
    def _map_to_pydantic_type(self, field_type: str) -> str:
        """映射字段类型到Pydantic类型"""
        type_mapping = {
            'string': 'str',
            'text': 'str',
            'int': 'int',
            'integer': 'int',
            'float': 'float',
            'bool': 'bool',
            'boolean': 'bool',
            'datetime': 'datetime'
        }
        return type_mapping.get(field_type.lower(), 'str')


class MigrationGenerationInput(BaseModel):
    """数据库迁移生成输入"""
    migration_name: str = Field(..., description="迁移文件名称")
    model_changes: str = Field(..., description="模型变更描述")
    auto_generate: bool = Field(default=True, description="是否自动生成迁移")


class MigrationGenerationTool(BaseTool):
    """数据库迁移生成工具"""
    name: str = "fastapi_migration_generator"
    description: str = "生成Alembic数据库迁移文件"
    args_schema: Type[BaseModel] = MigrationGenerationInput
    
    def _run(self, migration_name: str, model_changes: str, auto_generate: bool = True) -> str:
        """生成数据库迁移"""
        try:
            if auto_generate:
                # 执行alembic命令生成迁移
                import subprocess
                
                # 切换到backend目录
                backend_path = "/Users/chiyingjie/code/git/claude-fastapi/backend"
                
                cmd = ["alembic", "revision", "--autogenerate", "-m", migration_name]
                result = subprocess.run(
                    cmd, 
                    cwd=backend_path,
                    capture_output=True, 
                    text=True
                )
                
                if result.returncode == 0:
                    return f"✅ 成功生成迁移文件: {migration_name}\n输出: {result.stdout}"
                else:
                    return f"❌ 迁移生成失败: {result.stderr}"
            else:
                # 手动创建迁移模板
                migration_code = self._generate_migration_template(migration_name, model_changes)
                return f"✅ 生成迁移模板:\n\n{migration_code}"
                
        except Exception as e:
            return f"❌ 迁移生成失败: {str(e)}"
    
    def _generate_migration_template(self, migration_name: str, model_changes: str) -> str:
        """生成迁移代码模板"""
        return f'''"""
{migration_name}

Revision ID: auto_generated
Revises: 
Create Date: {datetime.now().isoformat()}

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'auto_generated'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    升级数据库
    
    变更内容: {model_changes}
    """
    # TODO: 实现升级逻辑
    pass


def downgrade():
    """
    回滚数据库
    """
    # TODO: 实现回滚逻辑
    pass
'''


# 导出所有工具
__all__ = [
    "APIGenerationTool",
    "ModelGenerationTool", 
    "CRUDGenerationTool",
    "SchemaGenerationTool",
    "MigrationGenerationTool"
]